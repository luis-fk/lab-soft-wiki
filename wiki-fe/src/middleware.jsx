import { NextResponse } from 'next/server';
import { getSession } from '@/lib/session';

export async function middleware(req) {
  const session = await getSession();
  const { pathname } = req.nextUrl;

  // Define the access control list, {route: [roles_with_access]}
  const accessControl ={
    '/admin': ['admin'],
    '/novo-artigo': ['admin', 'staff']
  };

  const restrictedAccess = accessControl[pathname];

  const notAccess = !restrictedAccess.includes(session.role);
 
  if (restrictedAccess && (!session || notAccess)) {
    return NextResponse.redirect(new URL('/', req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/admin/:path*', '/novo-artigo'],
};