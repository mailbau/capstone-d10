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
                    { label: 'Password', value: '', type: 'password' },
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

        const updatedData = {
            first_name: inputFields.find(field => field.label === 'First Name').value,
            last_name: inputFields.find(field => field.label === 'Last Name').value,
            user_email: inputFields.find(field => field.label === 'Email').value,
            user_password: inputFields.find(field => field.label === 'Password').value
        };

        const userId = jwtDecode(token).userId;

        try {
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
                fetchUserData(userId, token);
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
        <section className="flex flex-col items-center w-full max-w-2xl p-6 space-y-6 bg-white rounded-lg shadow-lg">
            <div className="flex flex-col items-center w-full mb-6">
                <h2 className="text-3xl font-bold text-gray-800">Profile Settings</h2>
                <p className="mt-2 text-gray-500">Update your personal details</p>
            </div>
            {userData && (
                <form onSubmit={handleSaveChanges} className="flex flex-col items-center w-full space-y-4">
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
                    <div className="flex justify-center space-x-4 mt-4">
                        <button
                            type="button"
                            onClick={toggleEditMode}
                            className="px-5 py-2 bg-blue-500 text-white rounded-full font-semibold hover:bg-blue-600 transition-colors"
                        >
                            {isEditing ? 'Cancel' : 'Edit'}
                        </button>
                        {isEditing && (
                            <button
                                type="submit"
                                className="px-5 py-2 bg-green-500 text-white rounded-full font-semibold hover:bg-green-600 transition-colors"
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
