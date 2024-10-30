import React from 'react';
import Header from '../../components/header';
import LoginForm from './loginform';
import Footer from '../../components/footer';

function LoginPage() {
    return (
        <div className="flex flex-col min-h-screen bg-gray-50">
            <Header />
            <main className="flex flex-1 justify-center items-center px-4 py-10">
                <LoginForm />
            </main>
            <Footer />
        </div>
    );
}

export default LoginPage;
