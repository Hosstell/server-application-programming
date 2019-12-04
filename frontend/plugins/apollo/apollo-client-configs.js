import { createHttpLink } from "apollo-link-http";
import {setContext} from "apollo-link-context";
import { from, split, concat, ApolloLink} from 'apollo-link'
import {createUploadLink} from 'apollo-upload-client'

export default function(context) {
  let opt = {
    uri: 'http://localhost:8000/graphql/',
    credentials: 'include'
  }

  let httpLink = split(
    operation => operation.getContext().hasUpload,
    createUploadLink(opt),
    new createHttpLink(opt)
  )

  const csrfMiddleware = setContext((_, { headers }) => {
    console.log(context.app.$cookies.get('csrftoken'))
    console.log(headers)
    return {
      headers: {
        ...headers,
        'X-CSRFToken': context.app.$cookies.get('csrftoken') || null
      }
    }
  })


  return {
    link: concat(csrfMiddleware, httpLink),
  }
}
