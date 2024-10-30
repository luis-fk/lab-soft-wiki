import React from 'react'
import Info from '@/components/info/Info'
import HowToHelp from '@/assets/json/how-to-help.json'

export const metadata = {
  title: 'Por que contribuir?',
}

export default function page() {
  return (
    <Info params={{ content: HowToHelp.content}} />
  )
}
