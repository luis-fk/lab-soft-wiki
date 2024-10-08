import Footer from '@/app/_components/layout/Footer';
import SignUp from '@/components/auth/SignUp';

export const metadata = {
  title: 'Cadastrar',
}

export default function SignUpPage() {
  return (
    <>
      <SignUp />

      <Footer />
    </>
  );
}