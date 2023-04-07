import React from 'react'
import {useForm} from 'react-hook-form';
import { yupResolver} from '@hookform/resolvers/yup';
import * as yup from 'yup';

export const Form = () =>{
    
    /*example for email and age would be like: yup.string().email().required(), or for age 
    yup.number().positive().integer().min(18).required()
    */
    const schema = yup.object().shape({
        name: yup.string().required("Name is required"),
        i1: yup.string(),
        i2: yup.string(),
        i3: yup.string()
        
    });

    const {register, handleSubmit, formState:{errors}} = useForm({
        resolver: yupResolver(schema)
    });

    const onSubmit = (data) => {
        console.log(data);
    };
    
/*age = number */
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
        <input type='text' placeholder='Name..'  {...register("name")} />
        <p>{errors.name?.message}</p>
        <input type='text' placeholder='i1..'  {...register("i1")} />
        <p>{errors.i1?.message}</p>
        <input type='text' placeholder='i2..'  {...register("i2")} />
        <p>{errors.i2?.message}</p>
        <input type='text' placeholder='i3..'  {...register("i3")} />
        <p>{errors.i3?.message}</p>
        <input type='submit' />
    </form>
  )
}

export default Form