"use client";

import React, { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import InputField from './inputfield';

function ProfileSettings() {
    const [userData, setUserData] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [inputFields, setInputFields] = useState([]);
    const [token, setToken] = useState(null);

    useEffect(() => {
        const storedToken = localStorage.getItem('token');
        if (storedToken) {
            setToken(storedToken);
            const decodedToken = jwtDecode(storedToken);
            const userId = decodedToken.userId;
            fetchUserData(userId, storedToken);
        }
    }, []);

    const fetchUserData = async (userId, token) => {
        try {
            const response = await fetch(`http://localhost:8080/user/${userId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                const data = await response.json();
                setUserData(data);
                setInputFields([
                    { label: 'First Name', value: data.first_name },
                    { label: 'Last Name', value: data.last_name },
                    { label: 'Email', value: data.user_email },
                    { label: 'Password', value: '', type: 'password' }, // Set an empty string for password
                ]);
            } else {
                console.error('Failed to fetch user data');
            }
        } catch (error) {
            console.error('Error fetching user data:', error);
        }
    };

    const handleSaveChanges = async (e) => {
        e.preventDefault();
        console.log('inputFields:', inputFields);

        const updatedData = {
            first_name: inputFields.find(field => field.label === 'First Name').value,
            last_name: inputFields.find(field => field.label === 'Last Name').value,
            user_email: inputFields.find(field => field.label === 'Email').value,
            user_password: inputFields.find(field => field.label === 'Password').value
        };


        console.log('Updated data:', updatedData);

        const userId = jwtDecode(token).userId;

        try {
            console.log('Updating user data...');
            const response = await fetch(`http://localhost:8080/user/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(updatedData),
            });

            if (response.ok) {
                setIsEditing(false);
                fetchUserData(userId, token); // Refresh data
            } else {
                console.error('Failed to update user data');
            }
        } catch (error) {
            console.error('Error updating user data:', error);
        }
    };

    const toggleEditMode = () => {
        setIsEditing(!isEditing);
    };

    return (
        <section className="flex overflow-hidden flex-col items-center w-full max-w-[960px] min-h-[695px] min-w-[240px] p-6">
            <div className="flex flex-col items-center w-full p-4">
                <h2 className="text-4xl font-bold tracking-tighter text-stone-900">Profile Settings</h2>
                <p className="mt-3 text-base text-stone-500">Update your personal details</p>
            </div>
            {userData && (
                <form onSubmit={handleSaveChanges} className="px-4 w-full max-w-md">
                    {inputFields.map((field, index) => (
                        <InputField
                            key={index}
                            label={field.label}
                            placeholder={field.placeholder}
                            type={field.type || 'text'}
                            value={field.value}
                            readOnly={!isEditing}
                            onChange={(e) => {
                                const updatedFields = [...inputFields];
                                updatedFields[index].value = e.target.value;
                                setInputFields(updatedFields);
                            }}
                        />
                    ))}
                    <div className="flex justify-center items-center py-3 w-full">
                        <button
                            type="button"
                            onClick={toggleEditMode}
                            className="px-5 py-3 bg-blue-600 rounded-3xl text-white font-bold max-w-[480px] mx-2"
                        >
                            {isEditing ? 'Cancel' : 'Edit'}
                        </button>
                        {isEditing && (
                            <button
                                type="submit"
                                className="px-5 py-3 bg-emerald-600 rounded-3xl text-white font-bold max-w-[480px] mx-2"
                            >
                                Save Changes
                            </button>
                        )}
                    </div>
                </form>
            )}
        </section>
    );
}

export default ProfileSettings;
