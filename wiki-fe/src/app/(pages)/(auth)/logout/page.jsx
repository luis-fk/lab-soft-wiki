'use client'
import React from 'react'
import { useRouter } from 'next/navigation';
import { terminateSession, getSession } from '@/app/_lib/session'

export default async function page() {
    const router = useRouter();
    const session = getSession();

    if(session){
        await terminateSession();
        router.push('/');
    }

    return <></>
}
