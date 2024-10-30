import React from 'react';
import Header from '../../components/header';
import RegisterForm from './registerform';
import Footer from '../../components/footer';

function RegisterPage() {
    return (
        <div className="flex flex-col min-h-screen bg-gray-50">
            <Header />
            <main className="flex flex-1 justify-center items-center px-4 py-10">
                <RegisterForm />
            </main>
            <Footer />
        </div>
    );
}

export default RegisterPage;
