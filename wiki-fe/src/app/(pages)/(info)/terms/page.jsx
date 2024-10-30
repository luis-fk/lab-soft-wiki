import React from 'react'
import Info from '@/components/info/Info'
import Terms from '@/assets/json/privacy-policy.json'

export const metadata = {
  title: 'Sobre a WikiDengue',
}

export default function page() {
  return (
    <Info params={{ content: Terms.terms}} />
  )
}
