class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            userInput: document.querySelector('#userInput'),
            faqContainer: document.getElementById("faq-container"),
            faqButton: document.getElementById("faq-button")
        };

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton, userInput, faqButton } = this.args;

        if (openButton) openButton.addEventListener('click', () => this.toggleState(chatBox));
        if (sendButton) sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        if (userInput) {
            userInput.addEventListener("keyup", ({ key }) => {
                if (key === "Enter") this.onSendButton(chatBox);
            });
            userInput.addEventListener("input", () => this.checkForWhatsapp(userInput.value.trim()));
        }

        if (faqButton) faqButton.addEventListener("click", () => this.showFAQ());
    }

    toggleState(chatbox) {
        this.state = !this.state;
        chatbox.classList.toggle('chatbox--active', this.state);
    }

    onSendButton(chatbox) {
        var textField = this.args.userInput;
        let text = textField.value.trim();
        if (!text) return;

        this.messages.push({ name: "User", message: text });
        this.updateChatText(chatbox);

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text }),
            headers: { 'Content-Type': 'application/json' }
        })
            .then(response => response.json())
            .then(data => {
                this.messages.push({ name: "Bot", message: data.answer });
                this.updateChatText(chatbox);

                // Jika respon chatbot mengandung kata tertentu, munculkan tombol FAQ
                if (data.faq_buttons) {
                    this.showFAQButtons(data.faq_buttons);
                }
            })
            .catch(error => console.error('Error:', error));

        textField.value = '';
    }

    updateChatText(chatbox) {
        const chatMessages = chatbox.querySelector('#messages');
        chatMessages.innerHTML = this.messages
            .map(msg => `<div class="messages__item ${msg.name === "Bot" ? "messages__item--visitor" : "messages__item--operator"}">${msg.message}</div>`)
            .join('');
    }

    checkForWhatsapp(value) {
        if (/^\+62\d{9,}$/.test(value)) {
            this.showFAQButton();
        }
    }

    showFAQButton() {
        if (this.args.faqContainer) this.args.faqContainer.style.display = "flex";
    }

    showFAQ() {
        if (this.args.faqContainer) this.args.faqContainer.style.display = "block";
    }

    sendFAQ(question) {
        this.args.userInput.value = question;
        this.onSendButton(this.args.chatBox);
    }

    showFAQButtons(faq_buttons) {
        const chatMessages = this.args.chatBox.querySelector('#messages');

        // Buat container untuk tombol FAQ
        const faqContainer = document.createElement("div");
        faqContainer.classList.add("faq-buttons");

        faq_buttons.forEach(faq => {
            const button = document.createElement("button");
            button.innerText = faq.text;
            button.classList.add("faq-button");
            button.onclick = () => this.sendFAQ(faq.value);
            faqContainer.appendChild(button);
        });

        chatMessages.appendChild(faqContainer);
    }
}

// Inisialisasi Chatbox
document.addEventListener("DOMContentLoaded", () => {
    const chatbox = new Chatbox();
    chatbox.display();
});
