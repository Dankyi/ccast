import React from 'react'
import {ChakraProvider, Stack, Avatar, AvatarBadge, Alert, AlertIcon, AlertTitle, AlertDescription, FormLabel, Input, FormHelperText, FormErrorMessage, Grid, Switch, InputGroup, InputRightElement, Icon, Flex, Text, Badge, Box, Image} from '@chakra-ui/react'

const App = () => (
  <ChakraProvider resetCSS>
    <Flex
    backgroundColor={"limegreen"}
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      textAlign="center"
      mt={4}
    >
      <Flex
        display="flex"
        flexDirection="row"
        alignItems="flex-start"
        justifyContent="flex-start"
      >
        <Text fontSize="3xl" fontWeight="bold">
          💱CCAST
        </Text>
        <Badge variant="subtle" colorScheme="pink" ml={1}>
          BETA
        </Badge>
      </Flex>
      <Text color="black">
        Crypto-currency Artificial Intelligence Stock Trader
      </Text>
    </Flex>
    <Grid p={10} gap={6} templateColumns="repeat(auto-fit, minmax(350px, 1fr))" backgroundColor={"gray"}>
      <Stack>
        <Box
          backgroundColor="white"
          boxShadow="sm"
          borderRadius="lg"
          pl={3}
          pr={3}
          pt={5}
          pb={5}
        >
          <Text>This is a test to check that data is displayed correctly</Text>
        </Box>
      </Stack>
      <Stack spacing={2}>
      <Box
          backgroundColor="white"
          boxShadow="sm"
          borderRadius="lg"
          pl={3}
          pr={3}
          pt={5}
          pb={5}
        >          <Stack spacing={2}>
            <Text>Here is an image:</Text>
          </Stack>
          <Image
            height="100px"
            width="100px"
            src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBYWFRgWFhUYGRgaGhweGBwcHBocHB4YGBgaGhgaGhocIS4lHB4rIRgYJjgmKy8xNTU1GiQ7QDs0Py40NTEBDAwMEA8QGhISHDEhISE0NDExNDQxNDQ0NDQxNDQ0MTE0NDQ0NDQ0NDQ0ND80ND8/MTE0MT8/MTQ/NDQxMTExMf/AABEIAOEA4QMBIgACEQEDEQH/xAAcAAACAgMBAQAAAAAAAAAAAAAEBQMGAAECBwj/xAA+EAABAwMCAwUGBAMIAgMAAAABAAIRAwQhMUEFElEGImFxgRORocHR8BQVMrFCUuEHI1OCkqKy8RZUJDRi/8QAGAEAAwEBAAAAAAAAAAAAAAAAAQIDAAT/xAAfEQEBAQEAAwEBAQEBAAAAAAAAAQIREiExAyJRQWH/2gAMAwEAAhEDEQA/AK1x22m7uvCq74rdxTijjWQnfabhj6dzXe6CKji9sdNM+oSu7H917lw6v9cdsk8YVsfggpZctgo9oQd03VXyltBTdO8I6m7yKWUXAFMqTJR16bMcXREgprwu6LC1wOQl1aku7UjSVLXuK5r2/gt4KtNucxnzTC4smVByvYHDx+q8o4Rx19EYON1beFdrQ/VR5ymue/BnEOznPSDGHl9m93KDOQY3VTvuF1aR77CB11HvV4bxxkxMLs8YY4QYM9RhNddpZmx501yIpvVtrU6T57jCPcl1Xh1HUO5fCUexvGl7X6JjwV3fcOtN/wDxQ7xTH8Uruzu2MfzTsR7xCOdSVtZvETXLm7uwxhJ1jChqXbGzGUg47fc8N0hCfW5SHiV057nOJySpLEFrfEoaoySiWGFaBUr3E7KIvaOhKHrVSZE46IUvVZ8TppQq6klWrsdUBqiP5TKo45wQQMK5dkgWMe+O8cCdh1UtezZ+Lne3raYlx8huqxfXrqhk4Gw2UN3ULnFziSVC0rZzIS6a5ZOdFceCP/u4GxVRVl7OXQ5XjxCG5/I5pzzLEL+as8Fi5+K9Iu27j7QkuEDnAHQB0x8VWLls00y7RCb26kzDxA2y0TCGblkeHyT/AKWeTYzfEitm5yoOIUYCJLgHZwF1eOaR4KuU9RWXgg4TLh9QHG37f0QlwA05Et3UrG8oDmd5vUfqHUEJ9TsLDC4bv9+qBfV5ThFB5I/Zao8Pe8w0fRJeQ+estaheY1lWvhtnyN5jgrjhvCWMAMd7cpo5hhc+qvm8+onPKnZUIGq5ZRO629gASGcPu3bIWrck7rKgMoaq0poyVryuslQMd1RDB4otxprChr2x5x0Ka0WKd9KdlvgWKDXpOY6CFITiVbL7hjXtncaKrXFAtPK4aK2NdS1CitUknoo6Rkrm5qSYCIsaMldHyInXDmSMjG3krVwdnceAYEJDaswIVk4c0BjnOgDT1XPq9qt9QsrGSsYMLuo4AqH20HSUe8qXOtvqjRH8KuS3nxqBHviSljBCJs35cP8A8n4Jbro5zw4/KH/4g/0/1WLf4t38xWIKFfaNn/zbrxc3/ihKX6PT5IztB/8Aeuv8p/2oF4imfL5Ke53Z8X+Irz6o5iDkIWvSIMsJ5TqOi3yEuKY2VqZ01VprhLOk1xRJ1RPDrB890+YVptuB88EjCsFlwtjBgSfihr9f8afmr/D+BzBcPGE7o2bW6NACNfT6KAO8POVK21SZ40y3GdlhYNlj3np5Lth02d5Lc61aa0qN48NUWzXIWqlH+i3jQmi19IDUJdc0ynF1RMcw9yX1WYytZw2ddLqZko62aSoWMzoEytqcj5LGtTUWeCKaw+KMtbWdkc20jX+ibxqfmUihCS9oeEF7C5uu4+itj6XRQObGEJ/NC3yjxepaFroIjKYWbQDCt3aTghd32NxvEKrjhr3Ek4GmuSumbmol43pvZ1WkwCn9w4NpN6kFVWyYWEMYN8p/xR5Aaw7ASk6bXwE92VyCouZdNKWwHbipbE9/zBHwQxcprN3fb5rcGGXtPBYt+z8ViXhkPHM39x4tYoiBywm3HKY9s8wJJ13iBCBYyfBN+meatDF7mQutuFSeY6eMJpbWrZwFxcuAwCpqZgKVvVJnhkxwDY0WnV4S32jjoTClpVDMH3rCNfUkYlQ41WnPHLmPkhTVbvH7ocDqes7oVxTcSfmPohecnQSpGXBByCFTMJo2t2k4OqY0KcjlPol1sOZsn0KZ2T5jwV5n0hdVBd2mPDdIb62ImNPuVcHkEJJxKl0U9ZUxqq1T1TqxpSRCSxyvhWDhlSCFOT2tq+j62p4wpHP2PuXLK4gFKeK3zWAku3hdOZOOW32ZVXg6FBVAQZS/hvEC+ebDduvuTQ0pHM1wKhuL4+In0w5pDt1Vb6xLHkSS06K3tad0Nd0WuEOHkp94eSKky27wjqiuMU4InUhNeH2YFSHTGxSrj9MNeQCf8xkqufc6n+l98KoWErCueZEsZKkt3Q5p8R+6gJUlNDpurF7NYovxPitoMIuZe8uI1UT6e2iI5lw9ocMapdXtbPovNHvDM+KJfT5QsbTI1Eon2Ti39iUsnT2guSCpWM11Hjr8FM+32Ig9VxRqEOg6FVzgl0EuK8DGTO+hSx95B2HUJzeWzJMST96JTV4S5xMHOyNwE2LsrpsgwnXt2uGjVSL+xuWgubBAzvOOiX2vHXMP94T5EEI5zQ1rr0BnEgwxEeuD6Jxw6sCJC83fxxjwADnzCa8L420AN5jPWVeXkRv1f3VBCVXTuaQgmcV5hg+S2x8ulR1rtVzOeyy+tS1wcBiYTC2YYBPRGVqQeGgdZlF2tuP0kZ6qanfQF90RgEpH2huzycxiBk+iccSpFhPwKpHam8JaQDtkeCri9vEtTgBva5zHQBIVw7N9qm1MB0OjI39y8zpuY5oHs2ggRzCe9O5BOvkstHuo1GuB0OvyVd/lLCZ3ZXv1tWDgoa7TphKOA8R52gzgjX0Tx55h18lxazx0ylzzidwcBR8btmPpB4xGuJz6Lp47ymonmDmOOHaea2dcHWexR6ogqKUZxWlyPLceefml4eqopF20oR9cDUoSrxAbYWk63kf+2WKr/mbv5gsTeNbyehv6hbGPE+9DvedQfd9FjHOn5aKVh4IZVneEZRPUcw8Ev5HAyWFF27dIkdE2YFpk2HN6eYSe8pgPxhOLYE4OfNYeGkvB6feVfKNoalRaQAZlR17Xp9E6qsDdUM8gkEGE9yXyJKrXAQEs4hwxjx3mifBWx9KRpPqgq9DEEAT4KVzynl68l4xwIsMsmNUqpVHtfmZXqN9ZYM5nGirV5wIufIGPcn8v9bntvgld7yAZ0GVebG3dEulVvs1ZchMg4VxZzRkgDqPnKhr3VY6iNCpmVtzqgLhxHj5LVOv11WGHNSgKrI32XmPa3hDmk6iSQvQqFyRClvLZlZvfAJ2P1WzrlbU7HiFPhr4kaz0J9U34RwF9Z7Q5pDW6nTxXoTOBs1jyjCaWFixuAI8T1XRf09IePstPBvZtaWCAAAQM+qKY/l6p9RoSI1Q1/wAPDRLR6KFzdKTXCh7JyomOyPNHNon+IqF9v3sKWs8VmulHayyPKHsaTjMdfJUupa3L8MZyjqT1XqpYHMLSNNMwkjrYNB5R3gYIPvBXV+GZqe3Nu2PP39nriYe+CuqPZif1PJ69Fe64AALi3qlz76g0y6o0DoDJ8NFfxiXlVd/8Vb1W03/OrX+d3uK2t4xvKibesPJMqILhsfLVVylcOBwExoXB1JPplcTsPWN8QVLTLNIM+aSsquHj+6JpXee9IRyno/pPG4j73U7LoDXVJGXTRoVK2vI1+SvlKw2rv5m4KU3EtySI6aldUKwGsZ9SjmUWPGkJ+dAvoXTice6EcJOo+/RdGz6Qj7RoZrHv+S3iHkC/Lg7MfRDV+GMEyPSFZJEJdevGiXWZwZqkdpYtYDG+uFI4jRFME/8ASjfb64mN1O4Umi2q/J2Qc5lGXFrvHrKDq42KTwp/OC6T50RVGu5pyk/MQYBhM7Spza5Q8KPke2zQ6CmDLcgaIThlPCfWzREHZPnP+p60GtaPou7qn3SjPZQonuGivM+k7VZpM5iZx4/RdvthGAj61CHSoHkDGVHefSmNFYcADOnivMu0HGavtHBjyGz/AA6L1S4t2uaQ4mCNivH+0LGtquaySAd0Px9D+k6W1Lh7v1PcfMkrjlW2NRFNi6ZUeIOQraM9ksRYxqViDhGW15OsKGvab7qK2dyHOnkuF1Q5t6snEge/5IynnU/OUpp1XbQjqVWdo8Z/ZGF0Ox1hdtrcoz9UMTGhxup6bw6Ruqyp1N+N5Y0PjA+KJt+IO00HWAq7cjMHCko1SDr7080Ti5UarSMa+YU7HCc/BILV/Q+aa29TO8eipL0tM/aQ1LK9WTAWru6jAcfggHXLxsD+6F+tDRlLEn4LPaPDSTrtHTxQ1rUMa+Y3C5vKgzBIPnEpvFulNTiJa88xER8VXr/tBGGpZ2k433yxoIjed1VKldxOStyRrVxZxrGYRFLjoBkHMdVR6BBd3imrRSDcSXbScf1RmZQuq9P4D2oa4hjiB0I6+KvVjcEgHHiZXz1aXwadJ9fdovYP7POL+3puY79dPfq06LeMDytXgFL7pxBwFP7WBkFKrm7k40S30aJ3VQUHWGVttULT3A7qO/amQ93TPI8jpj7C8l7Q02zOj5yJJ/de027ecEDKCr9krZ+arDLnazEYwJR/LPG3qPCGBE0gei9wp9jbRodNHEQBMmJyZ+9FPbdlbUEFlJnKMjfmdEb7BV9JdjxPlWL238htf/V/2j6rEWeY1AhH0QdFNaEOAkyeiPZQ6H9lwuyE4oub5Ipjz4hM/wADPUrb+HGMAysXVBU6/Kc6JhQqBpka/uh22zhqJhd+xOrQqROpb+zLxze5JKndOdvcntCtGHeiVcToSSfuFSQrKHGeWBr+yb2/EnkSAI9SVSqoPMp+EX7mv5C6Gn90YHFzuLp8YienKfqhfbvaCXAHy/qow8gSXYQ1W45DPNzDwEwjGOLO9B1n6Lnilx3CRt450Sv8UHYBgkIKpUDG958kzAVZU79UXiVSajjEZKXl5Tfi9rDi6dUoLdkKZzzqT2pUfIu2tKzJPa41Xof9kVy/8S4Anl5DPyXnfsCd16Z/ZbRLDUf1geaM+g9R4jehjDIJHVVuleczsJ1xBvOAMeKC/ChowB6KW77PmemMqnwUxYYmFHTZ4+ijuLhrIl3xSc6PxY+FMAb5o6o5uQ8tDT1IE+9J+F3gP8YOJCrf9qtu11Km8GHNdHSWuHxyrScife1dxd0249qwNG5e33arg8Rt26VqY699se6V89eyK7FBbjPoH88t/wD2KX+tqxfP34VbR4I/h9RsjWfNWG3qSBDSqTQqkFWfh/EHAQuF0xY6Mxkemyma+ccseqX2lzJmSmDq4I2+afMLWVWOGpn1hCPou2wDtsj6bmkZOVI+lzDUqshL6ILqjEHdLa7i7AkBWO5oNjO2/j8kouvLHVaQCK5pAZhLa3M3Le75a+9NLp0TKELBrOdkexhXDeIl7Yfq3UHfoQEV7ZxJ2HyVYuHPpPD/APpPLO/ZUbMwdwUWTVKbdeblJ3CCrnp3kS9gMEDHihKryAR4/BNnRbCriLTO2nuSa4p9E8uc6kygn05EI9GQpaxSFFvt1pluUW45tbcvcI0XrPZW15WNA0wqFwW3M49F6XwSiWtGyM/0tPqrRgaj4+9QlsZB+/muK2SDmeo+8qdj8RGfvIUte6aeojZUM5EFV3tJXc8loAcAM7OE9CrNVdiYVL4s5r3lwHK4YJBn7CGYOvgTgnFKtu7+J7Z0OoHRM+0HGjdU2M5C3lJJn4JR7eDD2wCf1DOvXoiqbdCMg9FUgKlw5Es4eEWwKVgWYJ+Ab4LEfCxFnnz5BlMeG3WQChXtlD0nuY6QuB0VeKBc6BkBN7e3aPnuqtYXTi3BHuR7HvOjvUlUyXUP3BrRIIhCv4pGEEymSe+cbphb06QEHPRUhLQJ4jnu58FDUrueSCzl8o+qe0qdIfpaCeuqiu6TTrHgE8n/AKXql39I7D3oFmCJ+yrFxFmDGiq1dx5iGiTulsPB1xbB7FWbmm9jpaSI0T+jcFogrL63Dm8wQ77awvtuOOAh7ZRD7pjgXA4+aSXzIcBEKa2uAJYd9D4o3oT6mqVxqoTdCMBTOoLqnYSjLVbgAbok6Iq2utJapvy7vQiafD4IR7RmDrs3ah5JGI+a9D4fRhsdFV+yVMNeGxrj6K/UaOpjK3S/rjxoRtLwRDKY1UsxqsFQFbiXQde2LwWB7WE6F2iUnsa6c3NMHyP1TWuxrzBEwofy6kf1NPoShNZjXOrFG7UvbZvNI1A98AiG93PUypuzfC3XDmFjwwva8xHd5mEAjGkzqrW/s7akFzmmemST6Li34DTYOZjX0+XIhxB8fJPPf/S8sJK1q+i9rLlj2DI52QWkjSHRuNirJYcBtqreZlZ7jExLZz1ELi/4BTqU3Bz35ye8cnqeqq9tw6rbuLWVTieQEGXNOwI0R5xpYtn/AIqP5n+8fRYq37e//wAOr7x9Vi3WUlQOaizT6KN4XC6XFC5c3fup7aXpdEO0Vfqslatq/If3TwKu1tdcw1HMpGVWgzJlV+3ug4S3CKoB75zEJpU7DkvmS10Fcg1HakEJYx4YcmSU5tLjmwACB4Kk+hYXX1NzzyDA3KW1rRrBjRWepABlV7iTC93gtppVerOLnQwY6rqjUczByN0ydbBuGhDvt5x70p+AeI8O5xzsMkZVefzB0wZBVwt3FmmnRTVLSlUiRDimlJz2RW9YOAIRVJ2VM7gDmGWOkbhdCxe3Vp/dbrpxqVxUfkFG24DlGzh1R8QwlP8AhPZis894Bg6k/JbyUmsz7THstbF9QYMNyT+yvbaZjumfDdBcG4c2i3kaJ6nr5poKYGQnkcv7b8tF9afJQzAJlMLymDmUhvqwDSAUm74wmZ5Vq3uQ5xAKLY6TlILfD+Ya5Tmi+QPNc3erX+UhcdtVjLstOchSNYo6jJWl1PgetfUja/PMR4AKEUgHF5btvqEJUcWEELo37+Vx9nz47xnPoF0/n+3fWk9/lz3ky5fFYkP5+/8AwHf6v6LFXyyl46Ud1JDuopkWBR+zzK45HQUPpIYs8E1uGwhzRgeaZgbLgtwE2s7wubEwllel0UdF7mrRlts6bSQXHX90Y0chkHBVetOJCBOvyTq0umv10GnmnhLBLiX5csrsa0dSdgttqA6bLpjBglNaHOFfsjJndcOopkWSSdyuTSCWm6UNo6rf4aYR1Gjk+anp0pdG4QYPb0nDqmlvRkTuspMR9GlgFFhllbt1hNG9xC2zdAj3iQBOU8hbRjDiVheIQ9vUIwVzWeE8pXdavA0Vev6kuOE513SS/ZDlzftrs4t+U4A5CDI2TK2uAGSZQTJ5hhE0Za7QkKWLyn1PRzbukea6LFzb1ARpClcQFeyWdR7yl1ywmVHw2tyPLTujnwUquqZDwQVHWVc059oOgWkB7U9ViXtNyPPmP6hSh3ggaFbGhRLHz4J5SWNPYHLiozC6cS09QVMCE8sbhU+iTPRBPaml6w+hWOt9OXRYCR9M+SKs7tzMIl9LqEM+nGo+KYD60vA5sjVHMqqo06/KcLt/E3t0yEWXRlTda55Cqdt2ggSRgao6x7QMe6CY89FmWUUQBK5tm5lcULtrmE8w0XVjVa7A1CPGMqdIInk7hjWUNQqgaqd9cASjIS0fbPx4ouu4FsgwUlF20aLs3ZcICa3gcomjfHfXquzUkyl7LaMqZ9QAJO2iKq3gYEG+4bqRJ6JFxDiHf1wl9TiRHropa908q1CtzHYBMKDhsqpbViWzJlOrB+MhLcmlPqDRupK9DcaKC1flMqT0c6s9BqFLmEKF7JTO8ocpkaFCETj4qnOl6G/DjofetJnyFYt4N5vFjqPvdFUv1LFiirU5281tuixYtAqO/wD0LKGg8lixUhQ9X9SFrrFiaAD3W6uixYixZS0f6qGjt5rFiI5Wnhv6CmnAf1lYsQn1tH9L+PzXNfRYsTppKWgRFBYsS6GGDELd6LFiIKnxb9ZS938PmFtYpX6aLJw3b72Tq0+q0sQrT6dWHzCY01ixLDf8d336R97JY3VYsVspUYsWLFUr/9k="
          />
        </Box>
      </Stack>
    </Grid>

    <Flex
    backgroundColor={"limegreen"}
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      textAlign="center"
      mt={4}
    >
  <Flex>
    <Text>
      Here is a footer!
    </Text>
  </Flex>
</Flex>

  </ChakraProvider>
)

export default App