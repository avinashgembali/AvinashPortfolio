import { Injectable } from '@angular/core';

export interface HeroSlide {
  greeting: string;
  name: string;
  subtitle: string;
  bg: string;
}

export interface Skill {
  name: string;
  percent: number;
}

export interface ServiceItem {
  icon: string;
  title: string;
  description: string;
}

export interface ResumeItem {
  year: string;
  title: string;
  org: string;
  description: string;
}

export interface Project {
  id: number;
  image: string;
  title: string;
  category: string;
  tags: string[];
  liveUrl?: string;
}

@Injectable({ providedIn: 'root' })
export class PortfolioService {

  heroSlides: HeroSlide[] = [
    {
      greeting: 'Hello!',
      name: "I'm Avinash Gembali",
      subtitle: 'Full Stack Developer & Software Engineer',
      bg: 'assets/images/bg_1.png',
    }
  ];

  skills: Skill[] = [
    { name: 'Angular', percent: 90 },
    { name: 'React', percent: 85 },
    { name: 'TypeScript', percent: 92 },
    { name: 'Node.js', percent: 88 },
    { name: 'Java', percent: 95 },
    { name: 'SQL / NoSQL', percent: 82 },
  ];

  services: ServiceItem[] = [
    {
      icon: '🖥️',
      title: 'Web Development',
      description: 'Building fast, scalable, and modern web applications using Angular, React, and Node.js.',
    },
    {
      icon: '📱',
      title: 'Mobile Development',
      description: 'Cross-platform mobile apps with React Native for seamless user experiences.',
    },
    {
      icon: '⚙️',
      title: 'Backend APIs',
      description: 'RESTful APIs with Node.js, Express — secure and performant.',
    }
  ];

  education: ResumeItem[] = [
    {
      year: '2022 – 2026',
      title: 'B.Tech in Computer Science',
      org: 'Anil Neerukonda Institute Of Technology And Sciences, Visakhapatnam',
      description: 'Graduated in Computer Science Engineering with a focus on software development, web technologies, and problem solving.',
    },
    {
      year: '2020 – 2022',
      title: 'Higher Secondary Education',
      org: 'Sri Chaitanya Junior College',
      description: 'Completed Intermediate education in Mathematics, Physics, and Chemistry (MPC).',
    },
    {
      year: '2019 – 2020',
      title: 'Secondary Education',
      org: 'Sri Chaitanya School',
      description: 'Completed Secondary School Education under the Andhra Pradesh State Board.',
    },
  ];

  experience: ResumeItem[] = [
    {
      year: 'July 2025 – Present',
      title: 'Software Developer Intern',
      org: 'InnCircles',
      description: 'Developed and maintained scalable web features, APIs, and dashboards for real-estate SaaS.',
    },
    {
      year: 'May 2025 – June 2025',
      title: 'Project Developer Intern',
      org: 'Logic While',
      description: 'Developed and maintained responsive web applications using Next.js, React, and Tailwind CSS, implementing secure authentication, integrating REST APIs, fixing bugs, optimizing performance, and collaborating with Git/GitHub.',
    },
  ];

  projects: Project[] = [
    { id: 1, image: 'assets/images/batbazaar.png', title: 'Bat Bazaar', category: 'Web App', tags: ['React', 'Node.js', 'MERN'], liveUrl: 'https://batbazaar-1.onrender.com/' },
    { id: 2, image: 'assets/images/helpermanagement.png', title: 'Helpers Management', category: 'Web App', tags: ['Angular', 'TypeScript', 'Node.js', 'MEAN'], liveUrl: 'https://helpersmodule-9spqqummo-avinashgembalis-projects.vercel.app/' },
  ];
}
