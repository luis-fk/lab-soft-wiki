import React from 'react'
import Info from '@/components/info/Info'
import About from '@/assets/json/about.json'

export const metadata = {
  title: 'Sobre a WikiDengue',
}

export default function page() {
  return (
    <Info params={{ content: About.about}} />
  )
}
