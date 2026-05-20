import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PortfolioService } from '../../services/portfolio.service';
import { ChatbotComponent } from '../chatbot/chatbot.component';

@Component({
  selector: 'app-hero',
  standalone: true,
  imports: [CommonModule, ChatbotComponent],
  templateUrl: './hero.component.html',
  styleUrl: './hero.component.css'
})
export class HeroComponent {
  chatOpen = false;
  prefillMessage = '';

  constructor(public portfolio: PortfolioService) {}

  get activeSlide() {
    return this.portfolio.heroSlides[0];
  }

  openChat(question: string) {
    this.prefillMessage = question;
    this.chatOpen = true;
  }

  scrollTo(anchor: string) {
    document.getElementById(anchor)?.scrollIntoView({ behavior: 'smooth' });
  }
}
