from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models.models import AnalyticsModel
from utils.database import analytics_collection

analytics_bp = Blueprint('analytics', __name__)


@analytics_bp.route('/analytics/track', methods=['POST'])
def track_event():
    """
    Track an analytics event
    POST /api/analytics/track
    Body: {
        "type": "page_view" | "project_click",
        "page": "/about",  // for page_view
        "project_id": "...",  // for project_click
        "project_title": "..."  // for project_click
    }
    """
    try:
        data = request.get_json()
        event_type = data.get('type')

        if event_type == 'page_view':
            event_doc = AnalyticsModel.create_page_view(
                page=data.get('page'),
                referrer=request.referrer,
                user_agent=request.headers.get('User-Agent')
            )
        elif event_type == 'project_click':
            event_doc = AnalyticsModel.create_project_click(
                project_id=data.get('project_id'),
                project_title=data.get('project_title')
            )
        else:
            return jsonify({"error": "Invalid event type"}), 400

        # Save to database
        analytics_collection.insert_one(event_doc)

        return jsonify({"message": "Event tracked successfully"}), 201

    except Exception as e:
        print(f"Error in track_event: {e}")
        return jsonify({"error": "Failed to track event"}), 500


@analytics_bp.route('/analytics/dashboard', methods=['GET'])
def get_dashboard_stats():
    """
    Get analytics dashboard statistics
    GET /api/analytics/dashboard?days=30
    """
    try:
        # Get number of days from query params (default 30)
        days = int(request.args.get('days', 30))
        start_date = datetime.utcnow() - timedelta(days=days)

        # Total page views
        total_page_views = analytics_collection.count_documents({
            "type": "page_view",
            "timestamp": {"$gte": start_date}
        })

        # Page views by page
        page_views_pipeline = [
            {"$match": {
                "type": "page_view",
                "timestamp": {"$gte": start_date}
            }},
            {"$group": {
                "_id": "$page",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]
        page_views = list(analytics_collection.aggregate(page_views_pipeline))
        page_views_formatted = [
            {"page": pv["_id"], "views": pv["count"]}
            for pv in page_views
        ]

        # Total project clicks
        total_project_clicks = analytics_collection.count_documents({
            "type": "project_click",
            "timestamp": {"$gte": start_date}
        })

        # Most clicked projects
        project_clicks_pipeline = [
            {"$match": {
                "type": "project_click",
                "timestamp": {"$gte": start_date}
            }},
            {"$group": {
                "_id": "$project_id",
                "title": {"$first": "$project_title"},
                "clicks": {"$sum": 1}
            }},
            {"$sort": {"clicks": -1}},
            {"$limit": 10}
        ]
        popular_projects = list(analytics_collection.aggregate(project_clicks_pipeline))
        popular_projects_formatted = [
            {
                "project_id": proj["_id"],
                "title": proj["title"],
                "clicks": proj["clicks"]
            }
            for proj in popular_projects
        ]

        # Daily page views (last 7 days)
        daily_views_pipeline = [
            {"$match": {
                "type": "page_view",
                "timestamp": {"$gte": datetime.utcnow() - timedelta(days=7)}
            }},
            {"$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$timestamp"
                    }
                },
                "views": {"$sum": 1}
            }},
            {"$sort": {"_id": 1}}
        ]
        daily_views = list(analytics_collection.aggregate(daily_views_pipeline))
        daily_views_formatted = [
            {"date": dv["_id"], "views": dv["views"]}
            for dv in daily_views
        ]

        # Unique visitors (approximation based on user agents)
        unique_visitors_pipeline = [
            {"$match": {
                "type": "page_view",
                "timestamp": {"$gte": start_date}
            }},
            {"$group": {
                "_id": "$user_agent"
            }},
            {"$count": "total"}
        ]
        unique_visitors_result = list(analytics_collection.aggregate(unique_visitors_pipeline))
        unique_visitors = unique_visitors_result[0]["total"] if unique_visitors_result else 0

        return jsonify({
            "period": f"Last {days} days",
            "total_page_views": total_page_views,
            "total_project_clicks": total_project_clicks,
            "unique_visitors": unique_visitors,
            "page_views_by_page": page_views_formatted,
            "popular_projects": popular_projects_formatted,
            "daily_views": daily_views_formatted
        }), 200

    except Exception as e:
        print(f"Error in get_dashboard_stats: {e}")
        return jsonify({"error": "Failed to fetch analytics"}), 500


@analytics_bp.route('/analytics/events', methods=['GET'])
def get_recent_events():
    """
    Get recent analytics events
    GET /api/analytics/events?limit=50
    """
    try:
        limit = int(request.args.get('limit', 50))

        events = list(
            analytics_collection.find()
            .sort("timestamp", -1)
            .limit(limit)
        )

        return jsonify({
            "events": [AnalyticsModel.serialize(e) for e in events]
        }), 200

    except Exception as e:
        print(f"Error in get_recent_events: {e}")
        return jsonify({"error": "Failed to fetch events"}), 500