"use client";

import { useRouter } from 'next/navigation';

function WithAuth({ children }) {
    const router = useRouter();
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

    if (!token) {
        // Redirect to login if user is not authenticated
        if (typeof window !== 'undefined') {
            router.push('/login');
        }
        return null; // Avoid rendering protected content while redirecting
    }

    return children;
}

export default WithAuth;
