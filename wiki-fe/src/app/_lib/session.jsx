'use server'
import { SignJWT, jwtVerify } from 'jose'
import { cookies } from 'next/headers'
 
const secretKey = 'secretKey'
const encodedKey = new TextEncoder().encode(secretKey)

export async function getSession() {
  const session = cookies().get('session')?.value;
  const payload = await decrypt(session);

  return payload;
}

export async function terminateSession() {
  const cookiesList = cookies();

  cookiesList.delete('session', {
    httpOnly: true,
    secure: true,
    sameSite: 'lax', 
    path: '/', 
  });
}
 
export async function encrypt(payload) {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('7d')
    .sign(encodedKey)
}
 
export async function decrypt(session) {
  try {
    const { payload } = await jwtVerify(session, encodedKey, {
      algorithms: ['HS256'],
    });

    return payload;
  } catch (error) {
    return null;
  }
}

export async function createSession(userId, role) {
  const expiresAt = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
  const session = await encrypt({ userId, role, expiresAt })
 
  cookies().set('session', session, {
    httpOnly: true,
    secure: true,
    expires: expiresAt,
    sameSite: 'lax',
    path: '/',
  })
}

export async function authenticate(formData) {
  /* autentica credenciais no back */
  console.log(formData.get('email'), formData.get('password'))
  if (formData.get('email') === 'admin@email.com') {
    return {errorMessage: 'Credenciais inválidas, por favor tente novamente'}
  } else {
    await createSession('1', 'admin')
    return {}
  }
  
}