#!/bin/bash
# Author:Andrey Nikishaev, IT4smart GmbH (Raphael Lekies)

DIST=$1
DIST_NO=$2


git tag -l | sort -u -r | while read TAG ; do
    #echo
    if [ $NEXT ];then
        echo "management-agent-it4smart (${NEXT#'v'}~${DIST_NO}) ${DIST}; urgency=low"
    fi
    GIT_PAGER=cat git log --no-merges --format="  * %s%n" $TAG..$NEXT

    if [ $NEXT ];then
        echo " -- IT4smart GmbH <support@it4smart.eu>  $(git log -n1 --no-merges --format='%aD' $NEXT)"
    fi
    NEXT=$TAG
done
FIRST=$(git tag -l | head -1)
echo
echo "management-agent-it4smart (${FIRST#'v'}~${DIST_NO}) ${DIST}; urgency=low"
GIT_PAGER=cat git log --no-merges --format="  * %s%n" $FIRST
echo " -- IT4smart GmbH <support@it4smart.eu> $(git log -n1 --no-merges --format='%aD' $FIRST)"
