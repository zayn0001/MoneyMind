// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import "firebase/auth"
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDSK1LXKkYKgs1vkOvVLlzUHf6u3jgYQCI",
  authDomain: "dues-35631.firebaseapp.com",
  databaseURL: "https://dues-35631-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "dues-35631",
  storageBucket: "dues-35631.appspot.com",
  messagingSenderId: "94288131228",
  appId: "1:94288131228:web:eed029c0463e15ebce2959",
  measurementId: "G-HJ8LVTE3CN"
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const auth = getAuth(app)