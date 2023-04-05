import React from 'react';
import '../styles/present.css';
import Form from '../components/Form';

function present() {
    return (
        <div className='present'>
            <h1 className='title'>Presentation</h1>
            {/* adding <Form/> here imports the Form from the Form.js file and makes it display on the "present" page */}
            <Form/>
            <div classname='display'>
                <p>Hello test</p>
            </div>
        </div>
    )
}

export default present