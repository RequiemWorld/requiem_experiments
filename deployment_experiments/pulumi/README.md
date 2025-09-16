

## Developer Experience Issues

- The digitalocean resources in Pulumi (and likely others) are obscure to use due to their design possibly not allowing for proper IDE support. [\[1\]](https://ibb.co/0Rn950jJ)
    - The available options for creation of resources can't easily be found within the IDE. Requiring referencing external resources to get anything done.
    - The digitalocean module (pydo) had a similar problem in our homebrew approach that was resolved by placing a cleaner interface in front of it. 
      - This is the reason why the homebrew approach was a preferred starting point over pulumi.

