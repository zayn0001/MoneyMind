"use client"
import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Margin } from "@mui/icons-material";

const provider = new GoogleAuthProvider();

const SignInButton = () => {
  const router = useRouter();

  const handleSignIn = () => {
    const auth = getAuth();
    signInWithPopup(auth, provider)
      .then((result) => {
        const credential = GoogleAuthProvider.credentialFromResult(result);
        const token = credential.accessToken;
        const user = result.user;
        router.push('/portfolio');
      })
      .catch((error) => {
        const errorCode = error.code;
        const errorMessage = error.message;
        const email = error.customData.email;
        const credential = GoogleAuthProvider.credentialFromError(error);
      });
  };

  return (
    <Button
      variant="outline" 
      onClick={handleSignIn} 
      style={{ backgroundColor: "white", color: "black" }}
    >
      Sign In
    </Button>
  );
};

export default SignInButton;
