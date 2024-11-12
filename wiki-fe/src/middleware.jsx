import { NextResponse } from 'next/server';
import { getSession } from '@/lib/session';

export async function middleware(req) {
  
  const session = await getSession();

  const { pathname } = req.nextUrl;
  
  if (!session) {
    return NextResponse.redirect(new URL('/', req.url));
  }

  // Define the access control list, {route: [roles_with_access]}
  const accessControl ={
    'admin': ['admin'],
    'novo-artigo': ['admin', 'staff'],
    'editar-artigo': ['admin', 'staff']
  };

  // primeira palavra depois do '/'
  const path = pathname.split('/')[1];
  
  const restrictedAccess = accessControl[path];

  const notAccess = !restrictedAccess.includes(session.role);
 
  if (restrictedAccess && notAccess) {
    return NextResponse.redirect(new URL('/', req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/admin/:path*', '/novo-artigo', '/editar-artigo/:path*'],
};