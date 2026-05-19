import { Component, ElementRef, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PortfolioService } from '../../services/portfolio.service';

@Component({
  selector: 'app-domains',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './domains.component.html',
  styleUrl: './domains.component.css'
})
export class DomainsComponent implements OnInit {
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
