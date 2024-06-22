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
    <div style={{justifyContent:"center", display:"flex", alignItems:"center", alignContent:"center", height:"100vh", flexDirection:"column"}}>
    <LargeText value={"Please Sign In"}/>
     <SignInButton />
    </div>
    </>
  );
};

export default GoogleSignIn;
