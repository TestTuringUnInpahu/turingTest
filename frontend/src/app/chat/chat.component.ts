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

  // Datos personales
  nombre: string = '';
  edad: number | null = null;
  nacionalidad: string = '';
  idioma: string = '';
  datosCompletos: boolean = false;

  // Opciones disponibles
  nacionalidades: string[] = ['Colombiana', 'Argentina', 'Mexicana', 'Peruana', 'Chilena', 'Venezolana'];
  idiomas: { nombre: string; codigo: string; }[] = [
    { nombre: 'Español', codigo: 'es' },
    { nombre: 'Inglés', codigo: 'en' },
    { nombre: 'Francés', codigo: 'fr' },
    { nombre: 'Alemán', codigo: 'de' },
    { nombre: 'Portugués', codigo: 'pt' }
  ];

  constructor(private http: HttpClient) {
    this.verificarDatos();
  }

  formValido(): boolean {
    return !!this.nombre && !!this.edad && !!this.nacionalidad;
  }

  enviarDatosPersonales() {
    if (this.formValido()) {
      const payload = {
        nombre: this.nombre,
        edad: this.edad,
        nacionalidad: this.nacionalidad,
        idioma: this.idioma
      };

      this.http.post('http://localhost:8000/datos_personales', payload).subscribe({
        next: res => {
          console.log('Datos personales enviados:', res);
          this.datosCompletos = true;
        },
        error: err => {
          console.error('Error al enviar datos personales:', err);
          this.datosCompletos = false;
        }
      });
    }
  }

  verificarDatos() {
    this.http.get('http://localhost:8000/verificar_datos').subscribe({
      next: res => {
        this.datosCompletos = true;
      },
      error: err => {
        this.datosCompletos = false;
      }
    });
  }

  async sendPrompt() {
    if (!this.datosCompletos) return;

    const userPrompt = this.prompt.trim();
    if (!userPrompt) return;

    this.messages.push({ text: userPrompt, sender: 'user' });
    this.prompt = '';
    this.loading = true;
    this.scrollToBottom();

    try {
      const res = await this.http.post<any>('http://localhost:8000/chat', { prompt: userPrompt }).toPromise();
      const delayMs = res.estimated_human_time_sec * 1000;
      await new Promise(resolve => setTimeout(resolve, delayMs));
      this.messages.push({ text: res.response, sender: 'bot' });
    } catch (error) {
      this.messages.push({ text: 'Ocurrió un error al contactar con el servidor.', sender: 'bot' });
    } finally {
      this.loading = false;
      this.scrollToBottom();
    }
  }

  scrollToBottom() {
    setTimeout(() => {
      this.chatWindow.nativeElement.scrollTop = this.chatWindow.nativeElement.scrollHeight;
    }, 100);
  }
}
