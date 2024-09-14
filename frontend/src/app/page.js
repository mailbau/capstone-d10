import Link from 'next/link';

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-4xl font-bold text-gray-900 mb-6">Welcome to Waste Management Solutions</h1>
      <p className="text-lg text-gray-700 mb-4">Your one-stop for managing waste effectively and efficiently.</p>
      <Link href="/login">
        <div className="px-6 py-2 text-white bg-green-500 rounded hover:bg-green-600 focus:outline-none">
          Go to Login
        </div>
      </Link>
    </div>
  );
}
