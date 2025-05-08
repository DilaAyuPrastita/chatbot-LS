# Tanpa pake NLP, jadi respon tetap, tidak menggunakan data json

import json

bot_name = "SikamBot"

# Jawaban langsung untuk FAQ
faq_answers = {
    "Bagaimana cara mengajukan pengajuan pendanaan?": """<div class='faq-jawab'>
        Berikut langkah-langkah mengajukan <a href='https://lahansikam.co.id/pinjaman/tata_cara' target='_blank'>pengajuan pendanaan</a>:
        <ul>
            <li>Pengajuan pendanaan dilakukan secara online.</li>
            <li>Kunjungi website <a href='https://lahansikam.co.id/' target='_blank'>Lahan Sikam</a>.</li>
            <li>Lengkapi dokumen yang diminta.</li>
            <li>Pihak Lahan Sikam akan melakukan verifikasi dokumen.</li>
            <li>Jika verifikasi berhasil, pihak Lahan Sikam akan menghubungi calon borrower.</li>
        </ul>
    </div>""",

    "Bagaimana cara memberikan pendanaan?": """<div class='faq-jawab'>
        Berikut langkah-langkah <a href='https://lahansikam.co.id/pendanaan/tata_cara' target='_blank'>memberikan pendanaan</a>:
        <ul>
            <li>Pemberian pendanaan dilakukan secara online.</li>
            <li>Kunjungi website <a href='https://lahansikam.co.id/' target='_blank'>Lahan Sikam</a>.</li>
            <li>Lengkapi dokumen yang diminta.</li>
            <li>Pihak Lahan Sikam akan melakukan verifikasi dokumen.</li>
            <li>Jika verifikasi berhasil, lender bisa mulai mendanai project di Lahan Sikam.</li>
        </ul>
    </div>""",

    "Progress pengajuan pendanaan sudah sampai mana?": """<div class='faq-jawab'>
        Untuk mengetahui progress pengajuan pendanaan Anda, dapat menghubungi CS kami melalui 
        <a href='https://wa.me/628117202500?text=Halo%2C%20saya%20ingin%20mengetahui%20progress%20pendanaan%20saya' class='wa-link' target='_blank'>WhatsApp</a> 
        atau email ke 
        <a href='mailto:info@lahansikam.co.id?subject=Permintaan%20Bantuan&body=Halo%2C%20saya%20ingin%20mengetahui%20progress%20pendanaan%20saya' class='email-link' target='_blank'>info@lahansikam.co.id</a>.
    </div>""",

    "Apa saja produk/layanan yang tersedia?": "<div class='faq-jawab'>Lahan Sikam memiliki 3 macam produk pendanaan, yaitu Pendanaan Mikro, Pendanaan Petani, dan Pendanaan Multiguna.</div>",

    "Berapa besar margin atau bunga pendanaan?": """<div class='faq-jawab'>
        Margin/bunga antara 2 - 2,5 % per bulan.<br>
        <strong>Note:</strong>
        <ul>
            <li> Dilihat dari hasil Credit Checking/Pefindo.</li>
            <li> Dilihat dari hasil scoring.</li>
        </ul>
    </div>""",

    "Berapa lama tenor/waktu pendanaan?": "<div class='faq-jawab'><a href='https://lahansikam.co.id/pendanaan/informasi' target='_blank'>Tenor</a> pendanaan dimulai dari 1 bulan hingga 12 bulan.</div>",

    "Bagaimana cara pembayarannya?": "<div class='faq-jawab'>Terdapat 3 <a href='https://lahansikam.co.id/pendanaan/informasi' target='_blank'>cara pembayaran</a>, yaitu Installment, Full Payment, dan Bullet Payment.</div>",

    "Apa syarat pengajuan pendanaan?": """<div class='faq-jawab'>
        Berikut <a href='https://lahansikam.co.id/pendanaan/informasi' target='_blank'>syarat</a> pengajuan pendanaan:
        <ul>
            <li>Usaha sudah berjalan minimal 2 tahun.</li>
            <li>Usia tidak lebih dari 60 tahun saat lunas.</li>
            <li>Usia minimal 21 tahun atau 18 tahun telah menikah.</li>
            <li>Warga Negara Indonesia (WNI).</li>
            <li>Tempat usaha dan tempat tinggal milik sendiri (salah satu boleh sewa).</li>
        </ul>
    </div>""",

    "Apa saja dokumen yang harus dilengkapi saat pengajuan pendanaan?": """<div class='faq-jawab'>
        Berikut <a href='https://lahansikam.co.id/pendanaan/informasi' target='_blank'>dokumen</a> yang harus disiapkan:
        <ul>
            <li>E-KTP</li>
            <li>NPWP (Pengajuan minimal 50jt)</li>
            <li>Kartu Keluarga</li>
            <li>Buku tabungan milik sendiri</li>
            <li>Mutasi rekening 3 bulan terakhir</li>
        </ul>
    </div>""",

    "Lain-lain": """<div class='faq-jawab'>
        Berikut informasi yang mungkin Anda butuhkan:
        <ul>
            <li><a href='https://wa.me/628117202500?text=Halo%2C%20saya%20ingin%20mengetahui%20informasi%20mengenai%20PARTNERSHIP' class='wa-link' target='_blank'>Partnership</a></li>
            <li><a href='https://wa.me/628117202500?text=Halo%2C%20saya%20ingin%20mengetahui%20informasi%20mengenai%20MAGANG' class='wa-link' target='_blank'>Magang</a></li>
            <li><a href='https://wa.me/628117202500?text=Halo%2C%20saya%20ingin%20mengetahui%20informasi%20mengenai%20PENELITIAN' class='wa-link' target='_blank'>Penelitian</a></li>
            <li><a href='https://wa.me/628117202500?text=Halo%2C%20saya%20ingin%20mengetahui%20informasi%20mengenai%20SOSIALISASI' class='wa-link' target='_blank'>Sosialisasi</a></li>
        </ul>
    </div>""",

    "Mengalami kendala": """<div class='faq-jawab'>
        Jika Anda mengalami kendala, silakan hubungi CS kami melalui:
        <ul>
            <li> JIka Anda mengalami kendala PENGAJUAN, hubungi CS kami melalui <a href='https://wa.me/628117202500?text=Halo%2C%20saya%20mengalami%20kendala%20pada%20proses%20PENGAJUAN' class='wa-link' target='_blank'>WhatsApp</a> atau email ke <a href='mailto:info@lahansikam.co.id?subject=Permintaan%20Bantuan&body=Halo%2C%20saya%20mengalami%20kendala%20pada%20proses%20PENGAJUAN'class='email-link' target='_blank'>info@lahansikam.co.id</a>.</li>
            <li> JIka Anda mengalami kendala PEMBAYARAN, hubungi CS kami melalui <a href='https://wa.me/628117202500?text=Halo%2C%20saya%20mengalami%20kendala%20pada%20proses%20PEMBAYARAN' class='wa-link' target='_blank'>WhatsApp</a> atau email ke <a href='mailto:info@lahansikam.co.id?subject=Permintaan%20Bantuan&body=Halo%2C%20saya%20mengalami%20kendala%20pada%20proses%20PEMBAYARAN'class='email-link' target='_blank'>info@lahansikam.co.id</a>.</li>
        </ul>
    </div>""",

    "Bagaimana cara menghubungi CS?": """<div class='faq-jawab'>
        Kamu bisa menghubungi CS melalui:
        <ul>
            <li><a href='https://wa.me/628117202500?text=Halo%2C%20saya%20butuh%20bantuan' class='wa-link' target='_blank'>WhatsApp</a></li>
            <li>Email ke <a href='mailto:info@lahansikam.co.id?subject=Permintaan%20Bantuan&body=Halo%2C%20saya%20ingin%20menanyakan%20tentang%20Lahan%20Sikam.' class='email-link' target='_blank'>info@lahansikam.co.id</a></li>
        </ul>
    </div>"""
}

def get_response(msg, user_stage):
    if user_stage == "ASK_NAME":
        return {"answer": "Terima kasih! Sekarang, bolehkah aku tahu nomor WhatsApp kamu?"}
    
    if user_stage == "ASK_PHONE":
        return {
            "answer": "Berikut adalah beberapa FAQ yang mungkin membantu:",
            "faq_buttons": [{"text": q, "value": q} for q in faq_answers.keys()] + [{"text": "Lihat FAQ", "value": "Lihat FAQ"}]
        }
    
    # Jika user memilih "Lihat FAQ"
    if msg == "Lihat FAQ":
        return {
            "answer": "Berikut adalah beberapa FAQ yang mungkin membantu:",
            "faq_buttons": [{"text": q, "value": q} for q in faq_answers.keys()] + [{"text": "Lihat FAQ", "value": "Lihat FAQ"}]
        }
    
    # Jika user memilih salah satu FAQ
    if msg in faq_answers:
        return {
            "answer": faq_answers[msg],
            "faq_buttons": [{"text": "Lihat FAQ", "value": "Lihat FAQ"}]  # Tambahkan tombol untuk kembali melihat FAQ
        }
    
    return {
        "answer": "Pertanyaan kamu tidak ditemukan. Kamu bisa menghubungi Customer Service kami melalui: <br>"
                  "<a href='https://wa.me/6281234567890?text=Halo%2C%20saya%20butuh%20bantuan' class='wa-link' target='_blank'>WhatsApp</a> atau "
                  "<a href='mailto:info@lahansikam.co.id?subject=Permintaan%20Bantuan&body=Halo%2C%20saya%20ingin%20menanyakan%20tentang%20Lahan%20Sikam.' class='email-link' target='_blank'>Email</a>.",
        "faq_buttons": [{"text": "Lihat FAQ", "value": "Lihat FAQ"}]
    }