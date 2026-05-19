import { Component, ElementRef, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PortfolioService } from '../../services/portfolio.service';

@Component({
  selector: 'app-skills',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './skills.component.html',
  styleUrl: './skills.component.css'
})
export class SkillsComponent implements OnInit {
  animated = false;

  constructor(public portfolio: PortfolioService, private el: ElementRef) {}

  ngOnInit() {
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(e => {
          if (e.isIntersecting) {
            e.target.classList.add('visible');
            this.animated = true;
          }
        });
      },
      { threshold: 0.2 }
    );
    setTimeout(() => {
      this.el.nativeElement.querySelectorAll('.animate-on-scroll').forEach((el: Element) => observer.observe(el));
    }, 100);
  }
}
