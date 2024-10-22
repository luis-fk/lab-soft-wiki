import { NextResponse } from 'next/server';
import { getSession } from '@/lib/session';

export async function middleware(req) {
  const session = await getSession();
  const { pathname } = req.nextUrl;

  const accessAdmin = pathname.startsWith('/admin') 
  const accessCreateArticle = pathname.startsWith('/novo-artigo')
  
  if (accessAdmin || accessCreateArticle) {
    if (!session || session.role === 'user') {
      return NextResponse.redirect(new URL('/', req.url));
    }
  }

  return NextResponse.next(); 
}

export const config = {
  matcher: ['/admin/:path*', '/novo-artigo'],
};
