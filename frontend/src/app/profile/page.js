import React from 'react';
import Header from '../../components/header';
import ProfileSettings from './profilesettings';
import WithAuth from '@/components/withAuth';

function ProfilePage() {
    return (
        <WithAuth>
            <div className="flex flex-col items-center w-full bg-gray-50 min-h-screen">
                <Header />
                <main className="flex flex-1 justify-center items-center p-10 w-full max-w-4xl">
                    <ProfileSettings />
                </main>
            </div>
        </WithAuth>
    );
}

export default ProfilePage;
