import { Component, ElementRef, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})

export class ChatComponent {
  @ViewChild('chatWindow') chatWindow!: ElementRef;
  prompt: string = '';
  loading: boolean = false;
  messages: { text: string, sender: 'user' | 'bot' }[] = [];

  constructor(private http: HttpClient) {}

  async sendPrompt() {
    const userPrompt = this.prompt.trim();
    if (!userPrompt) return;

    this.messages.push({ text: userPrompt, sender: 'user' });
    this.prompt = '';
    this.loading = true;
    this.scrollToBottom();

    try {
      const res = await this.http.post<any>('http://localhost:8000/chat', { prompt: userPrompt }).toPromise();
      
      const delayMs = res.estimated_human_time_sec * 1000;
      console.log(`Esperando ${delayMs} ms antes de mostrar respuesta...`);
  
      await new Promise(resolve => setTimeout(resolve, delayMs));
  
      this.messages.push({ text: res.response, sender: 'bot' });
      this.scrollToBottom();
    } catch (error) {
      this.messages.push({ text: 'Ocurrió un error al contactar con el servidor.', sender: 'bot' });
    } finally {
      this.loading = false;
    }
      
  }

  scrollToBottom() {
    setTimeout(() => {
      this.chatWindow.nativeElement.scrollTop = this.chatWindow.nativeElement.scrollHeight;
    }, 100);
  }
}
