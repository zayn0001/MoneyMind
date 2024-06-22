"use client"
import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
import 'firebase/auth';
import {app, auth} from '../config'; // Import your firebaseConfig here
import { Button } from "@/components/ui/button"
import { useRouter } from "next/navigation";
import LargeText from "../components/LargeText"

import SignInButton from "../components/SignInButton"

const GoogleSignIn = () => {

  return (
    <>
    <LargeText value={"Please Sign In"}/>
    <SignInButton />
    </>
  );
};

export default GoogleSignIn;
