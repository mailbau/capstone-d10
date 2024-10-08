"use client";

import React, { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';

function Header() {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);
    const router = useRouter();

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen);
    };

    // Handle clicks outside the dropdown
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsDropdownOpen(false); // Close dropdown if clicked outside
            }
        };

        // Add event listener when dropdown is open
        if (isDropdownOpen) {
            document.addEventListener('mousedown', handleClickOutside);
        }

        // Clean up event listener when component unmounts or dropdown closes
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [isDropdownOpen]); // Only re-run the effect when isDropdownOpen changes

    const handleLogOut = () => {

        router.push('/login');
    }

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
                <div className="relative flex gap-2 items-center">
                    <button className="flex justify-center items-center px-2.5 w-10 h-10 bg-lime-50 rounded-3xl" aria-label="Notification">
                        <img loading="lazy" src="/notification.svg" alt="Notification icon" />
                    </button>

                    {/* User button that toggles dropdown */}
                    <button
                        className="flex justify-center items-center px-2.5 w-10 h-10 bg-lime-50 rounded-3xl relative"
                        aria-label="User profile"
                        onClick={toggleDropdown}
                    >
                        <img loading="lazy" src="/user.svg" alt="User profile icon" className="object-contain w-5 aspect-square" />
                    </button>

                    {/* Dropdown menu */}
                    {isDropdownOpen && (
                        <div ref={dropdownRef} className="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-lg py-2 z-10">
                            <ul className="text-sm text-gray-700">
                                <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Profile</li>
                                <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Settings</li>
                                <li className="px-4 py-2 hover:bg-gray-100 cursor-pointer">Help</li>
                                <li
                                    className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                                    onClick={handleLogOut} // Log Out click handler
                                >
                                    Log Out
                                </li>
                            </ul>
                        </div>
                    )}
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
