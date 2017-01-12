#!/bin/bash
# Author:Andrey Nikishaev, IT4S GmbH (Raphael Lekies)
git tag -l | sort -u -r | while read TAG ; do
    #echo
    if [ $NEXT ];then
        echo "management-agent-it4s (${NEXT#'v'}) jessie; urgency=low"
    fi
    GIT_PAGER=cat git log --no-merges --format="  * %s%n" $TAG..$NEXT

    if [ $NEXT ];then
        echo " -- IT4S GmbH <support@it4s.eu>  $(git log -n1 --no-merges --format='%aD' $NEXT)"
    fi
    NEXT=$TAG
done
FIRST=$(git tag -l | head -1)
echo
echo "management-agent-it4s (${FIRST#'v'}) jessie; urgency=low"
GIT_PAGER=cat git log --no-merges --format="  * %s%n" $FIRST
echo " -- IT4S GmbH <support@it4s.eu> $(git log -n1 --no-merges --format='%aD' $FIRST)"
