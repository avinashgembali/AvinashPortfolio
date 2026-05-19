import { Component, ElementRef, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PortfolioService, Project } from '../../services/portfolio.service';

@Component({
  selector: 'app-projects',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './projects.component.html',
  styleUrl: './projects.component.css'
})
export class ProjectsComponent implements OnInit {
  activeFilter = signal('All');
  filters = ['All', 'Web App', 'Dashboard', 'Backend', 'Tool'];

  get filtered(): Project[] {
    const f = this.activeFilter();
    return f === 'All' ? this.portfolio.projects : this.portfolio.projects.filter(p => p.category === f);
  }

  constructor(public portfolio: PortfolioService, private el: ElementRef) {}

  ngOnInit() {
    const observer = new IntersectionObserver(
      entries => entries.forEach(e => e.isIntersecting && e.target.classList.add('visible')),
      { threshold: 0.1 }
    );
    setTimeout(() => {
      this.el.nativeElement.querySelectorAll('.animate-on-scroll').forEach((el: Element) => observer.observe(el));
    }, 100);
  }
}
