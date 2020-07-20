package com.example.test;

import java.nio.charset.StandardCharsets;
import java.util.Optional;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.amazonaws.services.imagebuilder.model.ServiceException;
import com.amazonaws.services.lambda.AWSLambda;
import com.amazonaws.services.lambda.AWSLambdaClientBuilder;
import com.amazonaws.services.lambda.model.InvokeRequest;
import com.amazonaws.services.lambda.model.InvokeResult;

public class HelloWorld {
    static Logger logger = Logger.getLogger(HelloWorld.class.getName());
    static String FUNCTION_NAME = "serverless-hello";

    public static void main(String... args) {
        invokeLambda();
    }

    public static void invokeLambda() {

        InvokeRequest invokeRequest = new InvokeRequest().withFunctionName(FUNCTION_NAME)
                .withPayload("{\n\"path\": \"my/path\",\n\"key2\": \"value2\",\n\"key3\": \"value3\"\n}");
        InvokeResult invokeResult = null;

        try {
            AWSLambda awsLambda = AWSLambdaClientBuilder.standard().build();

            invokeResult = awsLambda.invoke(invokeRequest);

            String ans = new String(invokeResult.getPayload().array(), StandardCharsets.UTF_8);

            // write out the return value
            logger.info(ans);

        } catch (ServiceException e) {
            logger.log(Level.SEVERE, e.getMessage(), e);
        }
        String s = Optional.ofNullable(invokeResult).map(InvokeResult::getStatusCode).map(String::valueOf)
                .orElse("None");
        logger.info(s);

    }

}
