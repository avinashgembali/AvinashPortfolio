import { Component, HostListener, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {
  scrolled = signal(false);
  menuOpen = signal(false);

  navLinks = [
    { label: 'Home', anchor: 'home' },
    { label: 'About', anchor: 'about' },
    { label: 'Resume', anchor: 'resume' },
    { label: 'Domains', anchor: 'domains' },
    { label: 'Skills', anchor: 'skills' },
    { label: 'Projects', anchor: 'projects' },
    { label: 'Contact', anchor: 'contact' },
  ];

  @HostListener('window:scroll')
  onScroll() {
    this.scrolled.set(window.scrollY > 50);
  }

  scrollTo(anchor: string) {
    const el = document.getElementById(anchor);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
    this.menuOpen.set(false);
  }

  toggleMenu() {
    this.menuOpen.update(v => !v);
  }
}
