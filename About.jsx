import React from 'react';

const About = () => {
  return (
    <section id="about" className="section bg-white">
      <div className="container">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-8">About Me</h2>

          <div className="space-y-6 text-lg text-gray-700 text-left">
            <p>
              I'm a passionate software engineer with a strong foundation in computer science
              and a love for creating innovative solutions. My journey in tech has been driven
              by curiosity and a desire to build applications that make a difference.
            </p>

            <p>
              With experience in both frontend and backend development, I enjoy working on
              full-stack projects that challenge me to learn and grow. I'm particularly
              interested in building scalable web applications, optimizing performance, and
              creating intuitive user experiences.
            </p>

            <p>
              When I'm not coding, you can find me exploring new technologies, contributing
              to open-source projects, or sharing my knowledge with the developer community.
              I believe in continuous learning and staying updated with the latest industry trends.
            </p>
          </div>

          {/* Education / Background */}
          <div className="mt-12 grid md:grid-cols-2 gap-8">
            <div className="card text-left">
              <h3 className="text-xl font-semibold mb-4 text-blue-600">Education</h3>
              <p className="text-gray-700">
                <strong>Bachelor's in Computer Science</strong><br />
                University Name<br />
                2020 - 2024
              </p>
            </div>

            <div className="card text-left">
              <h3 className="text-xl font-semibold mb-4 text-blue-600">Interests</h3>
              <ul className="text-gray-700 space-y-2">
                <li>• Full Stack Development</li>
                <li>• Cloud Computing</li>
                <li>• Open Source</li>
                <li>• Machine Learning</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;