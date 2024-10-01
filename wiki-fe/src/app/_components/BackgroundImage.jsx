import Image from 'next/image'
import saoJose from '@/assets/images/background.png'
import '@/styles/backgroundImage.css'
 
export default function BackgroundImage() {
  return (
    <Image
      className="background-image"
      alt="saoJose"
      src={saoJose}
      placeholder="blur"
      quality={100}
      fill
      sizes="100vw"
      style={{
        objectFit: 'cover',
      }}
    />
  )
}