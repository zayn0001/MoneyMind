// TextComponent.js
import { TypeAnimation } from 'react-type-animation';
 

const TextComponent = ({ value }) => {
  const seq = [value]
    return (
      <h1 className="scroll-m-20 text-4xl text-center font-extrabold tracking-tight lg:text-5xl m-5" >
        
        <TypeAnimation
  sequence={seq}
  speed={50}
  style={{ fontSize: '2em' }}
  repeat={0}
/>
      </h1>
    );
  };
  
  export default TextComponent;
  