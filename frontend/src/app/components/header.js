import React from 'react';

function Header() {
    return (
        <header className="flex justify-between items-center px-10 py-3.5 w-full border-b border-gray-200 min-h-[65px] max-md:px-5">
            <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                    <img loading="lazy" src="/logo.svg" alt="logo" className="object-contain w-4 aspect-square" />
                    <h1 className="text-lg font-bold tracking-tight leading-none text-stone-900">
                        Waste Management Dashboard
                    </h1>
                </div>
            </div>

            <nav className="flex items-center gap-8 max-md:hidden">
                <ul className="flex gap-9 items-center text-sm font-medium whitespace-nowrap text-stone-900">
                    <li>Dashboard</li>
                    <li>Routes</li>
                    <li>Settings</li>
                </ul>
                <div className="flex gap-2 items-center">
                    <button className="flex justify-center items-center px-2.5 w-10 h-10 bg-lime-50 rounded-3xl" aria-label="Notification">
                        <img loading="lazy" src="/notification.svg" alt="Notification icon" />
                    </button>
                    <button className="flex justify-center items-center px-2.5 w-10 h-10 bg-lime-50 rounded-3xl" aria-label="User profile">
                        <img loading="lazy" src="/user.svg" alt="User profile icon" className="object-contain w-5 aspect-square" />
                    </button>
                </div>
            </nav>

            <div className="flex items-center gap-4 md:hidden">
                <button className="flex justify-center items-center px-2.5 w-10 h-10 bg-lime-50 rounded-3xl" aria-label="Menu">
                    <img loading="lazy" src="/menu.svg" alt="Menu icon" className="object-contain w-5 aspect-square" />
                </button>
            </div>
        </header>
    );
}



export default Header;