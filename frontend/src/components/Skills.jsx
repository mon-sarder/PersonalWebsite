import React, { useState, useEffect } from 'react';
import { getSkills } from '../services/api';

const Skills = () => {
  const [skills, setSkills] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSkills();
  }, []);

  const fetchSkills = async () => {
    try {
      setLoading(true);
      const data = await getSkills(true); // Get grouped skills
      setSkills(data);
      setError(null);
    } catch (err) {
      setError('Failed to load skills');
      console.error('Error fetching skills:', err);
    } finally {
      setLoading(false);
    }
  };

  const getProficiencyColor = (proficiency) => {
    switch (proficiency) {
      case 'Expert':
        return 'bg-green-100 text-green-700';
      case 'Advanced':
        return 'bg-blue-100 text-blue-700';
      case 'Intermediate':
        return 'bg-yellow-100 text-yellow-700';
      case 'Beginner':
        return 'bg-gray-100 text-gray-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  if (loading) {
    return (
      <section id="skills" className="section bg-white">
        <div className="container">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">
            Skills & Technologies
          </h2>
          <div className="text-center text-gray-600">Loading skills...</div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section id="skills" className="section bg-white">
        <div className="container">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">
            Skills & Technologies
          </h2>
          <div className="text-center text-red-600">{error}</div>
        </div>
      </section>
    );
  }

  return (
    <section id="skills" className="section bg-white">
      <div className="container">
        <h2 className="text-4xl font-bold text-center text-gray-900 mb-4">
          Skills & Technologies
        </h2>
        <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
          A collection of technologies and tools I work with regularly.
        </p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {Object.entries(skills).map(([category, categorySkills]) => (
            <div key={category} className="card">
              <h3 className="text-xl font-semibold text-blue-600 mb-4">
                {category}
              </h3>
              <div className="space-y-3">
                {categorySkills.map((skill) => (
                  <div
                    key={skill.id}
                    className="flex justify-between items-center"
                  >
                    <span className="text-gray-700 font-medium">
                      {skill.name}
                    </span>
                    <span
                      className={`text-xs px-3 py-1 rounded-full ${getProficiencyColor(
                        skill.proficiency
                      )}`}
                    >
                      {skill.proficiency}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {Object.keys(skills).length === 0 && (
          <div className="text-center text-gray-600">
            No skills to display yet. Check back soon!
          </div>
        )}
      </div>
    </section>
  );
};

export default Skills;