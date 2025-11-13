import React, { useState, useEffect } from 'react';
import { FaGithub, FaExternalLinkAlt } from 'react-icons/fa';
import { getProjects, trackProjectClick } from '../services/api';

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      const data = await getProjects();
      setProjects(data);
      setError(null);
    } catch (err) {
      setError('Failed to load projects');
      console.error('Error fetching projects:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleProjectClick = (project) => {
    trackProjectClick(project.id, project.title);
  };

  if (loading) {
    return (
      <section id="projects" className="section bg-gray-50">
        <div className="container">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">
            My Projects
          </h2>
          <div className="text-center text-gray-600">Loading projects...</div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section id="projects" className="section bg-gray-50">
        <div className="container">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">
            My Projects
          </h2>
          <div className="text-center text-red-600">{error}</div>
        </div>
      </section>
    );
  }

  return (
    <section id="projects" className="section bg-gray-50">
      <div className="container">
        <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">
          My Projects
        </h2>
        <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
          Here are some of my recent projects that showcase my skills and experience
          in software development.
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {projects.map((project) => (
            <div key={project.id} className="card group">
              {/* Project Image Placeholder */}
              {project.image_url ? (
                <img
                  src={project.image_url}
                  alt={project.title}
                  className="w-full h-48 object-cover rounded-lg mb-4"
                />
              ) : (
                <div className="w-full h-48 bg-gradient-to-br from-blue-100 to-blue-200 rounded-lg mb-4 flex items-center justify-center">
                  <span className="text-blue-600 text-4xl font-bold">
                    {project.title.charAt(0)}
                  </span>
                </div>
              )}

              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {project.title}
              </h3>

              <p className="text-gray-600 mb-4 line-clamp-3">
                {project.description}
              </p>

              {/* Tech Stack */}
              <div className="flex flex-wrap gap-2 mb-4">
                {project.tech_stack.map((tech, index) => (
                  <span
                    key={index}
                    className="text-xs bg-blue-100 text-blue-700 px-3 py-1 rounded-full"
                  >
                    {tech}
                  </span>
                ))}
              </div>

              {/* Links */}
              <div className="flex gap-4">
                {project.github_link && (
                  <a
                    href={project.github_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={() => handleProjectClick(project)}
                    className="flex items-center gap-2 text-gray-700 hover:text-blue-600 transition-colors"
                  >
                    <FaGithub size={20} />
                    <span className="text-sm font-medium">Code</span>
                  </a>
                )}
                {project.live_link && (
                  <a
                    href={project.live_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={() => handleProjectClick(project)}
                    className="flex items-center gap-2 text-gray-700 hover:text-blue-600 transition-colors"
                  >
                    <FaExternalLinkAlt size={18} />
                    <span className="text-sm font-medium">Live Demo</span>
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>

        {projects.length === 0 && (
          <div className="text-center text-gray-600">
            No projects to display yet. Check back soon!
          </div>
        )}
      </div>
    </section>
  );
};

export default Projects;