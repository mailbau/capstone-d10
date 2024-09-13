import React from 'react';
import Header from '../components/header';
import LoginForm from './loginform';
import Footer from '../components/footer';

function WasteManagementDashboard() {
    return (
        <div className="flex flex-col bg-white">
            <div className="flex overflow-hidden flex-col w-full bg-white min-h-[841px] max-md:max-w-full">
                <div className="flex flex-col w-full min-h-[841px] max-md:max-w-full">
                    <Header />
                    <main className="flex justify-center items-start px-40 py-5 w-full min-h-[672px] max-md:px-5 max-md:max-w-full">
                        <LoginForm />
                    </main>
                    <Footer />
                </div>
            </div>
        </div>
    );
}

export default WasteManagementDashboard;