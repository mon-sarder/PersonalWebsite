import React from 'react';
import { FaGithub, FaLinkedin, FaEnvelope } from 'react-icons/fa';

const Hero = () => {
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section
      id="hero"
      className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-gray-100 pt-16"
    >
      <div className="container mx-auto px-4 text-center">
        <div className="fade-in">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-4">
            Hi, I'm <span className="text-blue-600">Mon Sarder</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            Software Engineer | Full Stack Developer
          </p>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-12">
            Passionate about building elegant solutions to complex problems.
            Specializing in modern web technologies and creating impactful user experiences.
          </p>

          {/* Call to Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <button
              onClick={() => scrollToSection('projects')}
              className="btn-primary"
            >
              View My Work
            </button>
            <button
              onClick={() => scrollToSection('contact')}
              className="btn-secondary"
            >
              Get In Touch
            </button>
          </div>

          {/* Social Links */}
          <div className="flex justify-center space-x-6">
            <a
              href="https://github.com/mon-sarder"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-blue-600 transition-colors"
            >
              <FaGithub size={28} />
            </a>
            <a
              href="https://www.linkedin.com/in/mon-sarder-946518392/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-blue-600 transition-colors"
            >
              <FaLinkedin size={28} />
            </a>
            <a
              href="mailto:mssarder.cpp.edu@gmail.com"
              className="text-gray-600 hover:text-blue-600 transition-colors"
            >
              <FaEnvelope size={28} />
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;