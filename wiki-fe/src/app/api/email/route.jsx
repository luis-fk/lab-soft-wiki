import { MailerSend, EmailParams, Sender, Recipient } from "mailersend";
import { NextResponse } from 'next/server';

export async function POST(req, res) {
    const { subject, email, content } = await req.json();
    
    const mailerSend = new MailerSend({
        apiKey: "mlsn.f05540cb84f723cd514c8a1a3e06e5084228c4a710220b36f4e25a67b9dab961",
    });

    const sentFrom = new Sender("MS_Z8gxHh@trial-0r83ql31emzgzw1j.mlsender.net", email);
    const recipients = [new Recipient("felipekorbes@usp.br", "Felipe Korbes")];

    const emailParams = new EmailParams()
        .setFrom(sentFrom)
        .setTo(recipients)
        .setReplyTo(sentFrom)
        .setSubject(subject)
        .setHtml(content)
        .setText(content);
    try {
        await mailerSend.email.send(emailParams);
        return NextResponse.json({ message: 'Email Enviado' });
    } catch (error) {
        return NextResponse.json({ message: 'Ocorreu algum erro ao enviar o email' });
    }
}
