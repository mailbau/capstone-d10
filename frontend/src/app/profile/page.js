import React from 'react';
import Header from '../../components/header';
import ProfileSettings from './profilesettings';

function ProfilePage() {
    return (
        <div className="flex flex-col items-center w-full bg-gray-50 min-h-screen">
            <Header />
            <main className="flex flex-1 justify-center items-center p-10 w-full max-w-4xl">
                <ProfileSettings />
            </main>
        </div>
    );
}

export default ProfilePage;
