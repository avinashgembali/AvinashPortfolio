import { Component } from '@angular/core';
import { PortfolioService } from '../../services/portfolio.service';

@Component({
  selector: 'app-hero',
  standalone: true,
  imports: [],
  templateUrl: './hero.component.html',
  styleUrl: './hero.component.css'
})
export class HeroComponent {
  constructor(public portfolio: PortfolioService) {}

  get activeSlide() {
    return this.portfolio.heroSlides[0];
  }

  scrollTo(anchor: string) {
    document.getElementById(anchor)?.scrollIntoView({ behavior: 'smooth' });
  }
}
