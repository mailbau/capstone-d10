"use client";

import React, { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import InputField from './inputfield';

function ProfileSettings() {
    const [userData, setUserData] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [isPasswordVerified, setIsPasswordVerified] = useState(false);
    const [currentPassword, setCurrentPassword] = useState('');
    const [inputFields, setInputFields] = useState([]);
    const [token, setToken] = useState(null);
    const [successMessage, setSuccessMessage] = useState(''); // Success message state

    useEffect(() => {
        const storedToken = localStorage.getItem('token');
        if (storedToken) {
            setToken(storedToken);
            const decodedToken = jwtDecode(storedToken);
            const userId = decodedToken.userId;
            fetchUserData(userId, storedToken);
        }
    }, []);

    const fetchUserData = async (userId, token, password = null) => {
        try {
            const headers = {
                Authorization: `Bearer ${token}`,
            };
            if (password) {
                headers['X-Current-Password'] = password;
            }

            // const response = await fetch(`http://localhost:8080/user/${userId}`, { headers });
            const response = await fetch(`https://capstoned10.duckdns.org/user/${userId}`, { headers });

            if (response.ok) {
                const data = await response.json();
                setUserData(data);
                setInputFields([
                    { label: 'First Name', value: data.first_name },
                    { label: 'Last Name', value: data.last_name },
                    { label: 'Email', value: data.user_email },
                ]);

                if (password) {
                    setIsPasswordVerified(true);
                }
            } else {
                console.error('Failed to fetch user data or password incorrect');
                if (password) {
                    alert('Password verification failed. Please try again.');
                }
            }
        } catch (error) {
            console.error('Error fetching user data:', error);
        }
    };

    const verifyCurrentPassword = () => {
        const userId = jwtDecode(token).userId;
        fetchUserData(userId, token, currentPassword);
    };

    const handleSaveChanges = async (e) => {
        e.preventDefault();

        const updatedData = {
            first_name: inputFields.find(field => field.label === 'First Name').value,
            last_name: inputFields.find(field => field.label === 'Last Name').value,
            user_email: inputFields.find(field => field.label === 'Email').value,
        };

        const userId = jwtDecode(token).userId;

        try {
            // const response = await fetch(`http://localhost:8080/user/${userId}`, {
            const response = await fetch(`https://capstoned10.duckdns.org/user/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(updatedData),
            });

            if (response.ok) {
                setIsEditing(false);
                setIsPasswordVerified(false);
                setCurrentPassword('');
                setSuccessMessage('Profile updated successfully!'); // Set success message
                fetchUserData(userId, token); // Refresh data

                // Clear success message after 3 seconds
                setTimeout(() => {
                    setSuccessMessage('');
                }, 3000);
            } else {
                console.error('Failed to update user data');
            }
        } catch (error) {
            console.error('Error updating user data:', error);
        }
    };

    const toggleEditMode = () => {
        setIsEditing(!isEditing);
        setIsPasswordVerified(false);
        setCurrentPassword('');
    };

    return (
        <section className="flex flex-col items-center w-full max-w-2xl p-6 space-y-6 bg-white rounded-lg shadow-lg">
            <div className="flex flex-col items-center w-full mb-6">
                <h2 className="text-3xl font-bold text-gray-800">Profile Settings</h2>
                <p className="mt-2 text-gray-500">Update your personal details</p>
            </div>
            {userData && (
                <form onSubmit={handleSaveChanges} className="flex flex-col items-center w-full space-y-4">
                    {/* Display Basic Info */}
                    {inputFields.map((field, index) => (
                        <InputField
                            key={index}
                            label={field.label}
                            placeholder={field.placeholder}
                            type={field.type || 'text'}
                            value={field.value}
                            readOnly={!isPasswordVerified}
                            onChange={(e) => {
                                const updatedFields = [...inputFields];
                                updatedFields[index].value = e.target.value;
                                setInputFields(updatedFields);
                            }}
                        />
                    ))}

                    {/* Current Password Verification */}
                    {isEditing && !isPasswordVerified && (
                        <div className="w-full px-4 py-3 max-w-lg">
                            <InputField
                                label="Enter Current Password"
                                placeholder="Enter current password"
                                type="password"
                                name="currentPassword"
                                value={currentPassword}
                                onChange={(e) => setCurrentPassword(e.target.value)}
                            />
                            <button
                                type="button"
                                onClick={verifyCurrentPassword}
                                className="w-full mt-4 px-5 py-2 bg-blue-500 text-white rounded-full font-semibold hover:bg-blue-600 transition-colors"
                            >
                                Verify Password
                            </button>
                        </div>
                    )}

                    <div className="flex justify-center space-x-4 mt-4">
                        <button
                            type="button"
                            onClick={toggleEditMode}
                            className="px-5 py-2 bg-blue-500 text-white rounded-full font-semibold hover:bg-blue-600 transition-colors"
                        >
                            {isEditing ? 'Cancel' : 'Edit'}
                        </button>
                        {isEditing && isPasswordVerified && (
                            <button
                                type="submit"
                                className="px-5 py-2 bg-green-500 text-white rounded-full font-semibold hover:bg-green-600 transition-colors"
                            >
                                Save Changes
                            </button>
                        )}
                    </div>

                    {/* Success Message */}
                    {successMessage && (
                        <div className="mt-4 p-3 text-green-800 bg-green-100 border border-green-300 rounded-lg text-center">
                            {successMessage}
                        </div>
                    )}
                </form>
            )}
        </section>
    );
}

export default ProfileSettings;
