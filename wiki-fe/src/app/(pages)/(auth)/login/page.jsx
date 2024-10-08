import Footer from '@/app/_components/layout/Footer';
import Login from '@/components/auth/Login';

export const metadata = {
  title: 'Login',
}

export default function SignUpPage({errorMessage}) {
  return (
    <>
      <Login params={errorMessage} />

      <Footer />
    </>
  );
}