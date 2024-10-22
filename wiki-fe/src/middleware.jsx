import { NextResponse } from 'next/server';
import { getSession } from '@/lib/session';

export async function middleware(req) {
  const session = await getSession();
  const { pathname } = req.nextUrl;

  if (pathname.startsWith('/admin')) {
    if (!session || session.role !== 'admin') {
      return NextResponse.redirect(new URL('/', req.url));
    }
  }

  return NextResponse.next(); 
}

export const config = {
  matcher: ['/admin/:path*'],
};
