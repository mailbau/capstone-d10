import React from 'react';
import Header from '../../components/header';
import ProfileSettings from './profilesettings';

function ProfilePage() {
    return (
        <div className="flex flex-col bg-white">
            <div className="flex overflow-hidden flex-col w-full bg-white min-h-[800px] max-md:max-w-full">
                <Header />
                <main className="flex flex-1 justify-center items-center px-40 py-5 max-md:px-5 max-md:max-w-full">
                    <ProfileSettings />
                </main>
            </div>
        </div>
    );
}

export default ProfilePage;