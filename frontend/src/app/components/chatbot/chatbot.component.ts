import { Component, EventEmitter, Input, OnInit, Output, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService, ChatMessage } from '../../services/chat.service';

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent implements OnInit, AfterViewChecked {
  @Input() prefillMessage = '';
  @Output() close = new EventEmitter<void>();
  @ViewChild('messageContainer') messageContainer!: ElementRef;

  messages: ChatMessage[] = [
    { role: 'bot', text: "Hi! I'm Avinash's AI assistant. Ask me anything about his skills, projects, or experience!" }
  ];
  userInput = '';
  isLoading = false;

  constructor(private chatService: ChatService) {}

  ngOnInit() {
    if (this.prefillMessage) {
      this.userInput = this.prefillMessage;
      this.send();
    }
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  send() {
    const text = this.userInput.trim();
    if (!text || this.isLoading) return;

    this.messages.push({ role: 'user', text });
    this.userInput = '';
    this.isLoading = true;

    this.chatService.ask(text).subscribe({
      next: (res) => {
        this.messages.push({ role: 'bot', text: res.answer });
        this.isLoading = false;
      },
      error: () => {
        this.messages.push({ role: 'bot', text: 'Sorry, I could not connect to the server. Please try again.' });
        this.isLoading = false;
      }
    });
  }

  onKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.send();
    }
  }

  private scrollToBottom() {
    try {
      this.messageContainer.nativeElement.scrollTop = this.messageContainer.nativeElement.scrollHeight;
    } catch {}
  }
}
